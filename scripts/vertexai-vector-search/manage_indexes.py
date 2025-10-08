"""
VertexAI Vector Search Infrastructure Setup
Creates indexes, endpoints, and deployments for databases
"""

import os
import logging
import argparse
from typing import Dict
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv

from google.cloud import aiplatform
from google.cloud.aiplatform import MatchingEngineIndex, MatchingEngineIndexEndpoint
from google.cloud import storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

@dataclass
class IndexConfig:
    """Configuration for a Vector Search index"""
    name: str
    display_name: str
    description: str
    dimensions: int
    shard_size: str
    machine_type: str


@dataclass
class InfrastructureDetails:
    """Store infrastructure details"""
    index_id: str
    index_resource_name: str
    endpoint_id: str
    endpoint_resource_name: str
    deployed_index_id: str
    created_at: str
    config_type: str


class VectorSearchInfrastructure:
    """Manages VertexAI Vector Search infrastructure creation and deployment"""
    
    CONFIGS = {
        "columns": IndexConfig(
            name="columns",
            display_name="Column-Schema-Index",
            description="Index for database column schemas and metadata",
            dimensions=3072,
            shard_size="SHARD_SIZE_SMALL", # See https://cloud.google.com/vertex-ai/docs/vector-search/create-manage-index#index_size
            machine_type="e2-standard-2"   # See https://cloud.google.com/vertex-ai/docs/vector-search/create-manage-index#index_size
        ),
        "docs": IndexConfig(
            name="docs",
            display_name="Documentation-Index",
            description="Index for PDF documentation chunks",
            dimensions=3072,
            shard_size="SHARD_SIZE_SMALL", # See https://cloud.google.com/vertex-ai/docs/vector-search/create-manage-index#index_size
            machine_type="e2-standard-2"   # See https://cloud.google.com/vertex-ai/docs/vector-search/create-manage-index#index_size
        )
    }
    
    
    def __init__(
        self,
        project_id: str,
        region: str = "us-east1"
    ):
        """
        Initialize the infrastructure manager
        
        Args:
            project_id: GCP project ID
            region: GCP region for resources
        """
        self.project_id = project_id
        self.region = region
        
        aiplatform.init(project=project_id, location=region)
        self.storage_client = storage.Client(project=project_id)        
        self.infrastructure: Dict[str, InfrastructureDetails] = {}
        
        logger.info(f"Initialized VectorSearchInfrastructure for project: {project_id}, region: {region}")
    
    
    def _create_index(
        self,
        config_type: str
    ) -> MatchingEngineIndex:
        """
        Create a Vector Search index
        
        Args:
            config_type: Type of index (columns or docs)
            
        Returns:
            Created MatchingEngineIndex instance
        """
        config = self.CONFIGS[config_type]
        index_name = "esma-vector-search-index"
        # JSON files inside GCS directory need to be in a specific format: 
        # https://cloud.google.com/vertex-ai/docs/vector-search/format-structure#data-file-formats
        gcs_uri = "gs://sql-multiagent-column-vectors"
        shard_size = config.shard_size
        
        logger.info(f"Creating index: {index_name}")
        
        try:
            index = MatchingEngineIndex.create_tree_ah_index(
                display_name = f"esma-vector-search-index-{config.name}",
                description  = f"{config.description} for esma-vector-search-index",
                dimensions   = config.dimensions,
                approximate_neighbors_count = 75,
                index_update_method = "BATCH_UPDATE",
                shard_size = shard_size,
                contents_delta_uri = gcs_uri,
                distance_measure_type = (
                    aiplatform
                    .matching_engine
                    .matching_engine_index_config
                    .DistanceMeasureType
                    .DOT_PRODUCT_DISTANCE
                ),
            )
            
            logger.info(f"Successfully created index: {index.display_name} (ID: {index.name})")
            return index
            
        except Exception as e:
            logger.error(f"Failed to create index {index_name}: {e}")
            raise


    def _create_endpoint(
        self,
        config_type: str,
    ) -> MatchingEngineIndexEndpoint:
        """
        Create an index endpoint for serving queries
        
        Args:
            config_type: Type of index
            
        Returns:
            Created MatchingEngineIndexEndpoint instance
        """
        endpoint_name = f"esma-vector-search-index-{config_type}-endpoint"
        
        logger.info(f"Creating endpoint: {endpoint_name}")
        
        try:
            endpoint = MatchingEngineIndexEndpoint.create(
                display_name = endpoint_name,
                description = f"Endpoint for esma-vector-search-index {config_type} index",
                public_endpoint_enabled = True
            )
            
            logger.info(f"Successfully created endpoint: {endpoint.display_name} (ID: {endpoint.name})")
            return endpoint
            
        except Exception as e:
            logger.error(f"Failed to create endpoint {endpoint_name}: {e}")
            raise
    
    
    def _deploy_index_to_endpoint(
        self,
        index: MatchingEngineIndex,
        endpoint: MatchingEngineIndexEndpoint,
        config_type: str
    ) -> str:
        """
        Deploy an index to an endpoint
        
        Args:
            index: The index to deploy
            endpoint: The endpoint to deploy to
            config_type: Type of index
            
        Returns:
            Deployed index ID
        """
        config = self.CONFIGS[config_type]
        deployed_index_id = f"esma_vector_search_index_{config_type}"
        machine_type = config.machine_type
        
        logger.info(f"Deploying index {index.display_name} to endpoint {endpoint.display_name}")
        
        try:
            endpoint.deploy_index(
                index=index,
                deployed_index_id=deployed_index_id,
                machine_type=machine_type,
                min_replica_count=1, # Minimum number of machine replicas for low latency and high availability
                max_replica_count=3  # Maximum number of machine replicas to handle load spikes (cost control)
            )
                        
            logger.info(f"Successfully deployed index to endpoint with ID: {deployed_index_id}")
            return deployed_index_id
            
        except Exception as e:
            logger.error(f"Failed to deploy index: {e}")
            raise
    
    
    def setup_infrastructure_for_database(
        self,
        config_type: str
    ) -> InfrastructureDetails:
        """
        Set up complete infrastructure for a database and type
        
        Args:
            database: Database name
            config_type: Type of index (columns or docs)
            
        Returns:
            InfrastructureDetails with all resource information
        """
        logger.info(f"Setting up infrastructure - {config_type}")
        
        index = self._create_index(config_type)
        endpoint = self._create_endpoint(config_type)        
        deployed_id = self._deploy_index_to_endpoint(index, endpoint, config_type)
        
        details = InfrastructureDetails(
            index_id=index.name.split("/")[-1],
            index_resource_name=index.resource_name,
            endpoint_id=endpoint.name.split("/")[-1],
            endpoint_resource_name=endpoint.resource_name,
            deployed_index_id=deployed_id,
            created_at=datetime.now().isoformat(),
            config_type=config_type
        )
        
        key = f"esma-vector-search-index-{config_type}"
        self.infrastructure[key] = details
        
        logger.info(f"Infrastructure setup complete for {key}")
        return details
    

    def update_column_embeddings(self) -> None:
        """Update a vector search index with new embeddings from GCS"""
        gcs_uri: str = "gs://sql-multiagent-column-vectors"
        index_name = "projects/514700908055/locations/us-east1/indexes/2137666108675588096"
        index = aiplatform.MatchingEngineIndex(index_name=index_name)
        index.update_embeddings(
            contents_delta_uri=gcs_uri, 
            is_complete_overwrite=False
        )
        logger.info(f"Updated columns embeddings from {gcs_uri}")
    
    
    def get_infrastructure_status(self) -> None:
        """Print current infrastructure status"""
        print("\n" + "="*50)
        print("VECTOR SEARCH INFRASTRUCTURE STATUS")
        print("="*50)
        print(f"Project: {self.project_id}")
        print(f"Region: {self.region}")
        print("\nCreated Resources:")
        print("-"*50)
        
        for key, details in self.infrastructure.items():
            print(f"\n{key.upper()}:")
            print(f"  Index ID: {details.index_id}")
            print(f"  Endpoint ID: {details.endpoint_id}")
            print(f"  Deployed Index ID: {details.deployed_index_id}")
            print(f"  Created: {details.created_at}")
        
        if not self.infrastructure:
            print("No resources created yet")
        
        print("\n" + "="*50)


def main():
    """Main function to run infrastructure setup"""
    parser = argparse.ArgumentParser(description="Set up VertexAI Vector Search infrastructure")
    parser.add_argument("--type", choices=["columns", "docs"], help="Specific type to setup")
    parser.add_argument("--create", action="store_true", help="Flag to create infrastructure", default=False)
    parser.add_argument("--update", action="store_true", help="Flag to update infrastructure", default=False)
    
    args = parser.parse_args()

    if args.create:
        infra = VectorSearchInfrastructure(
            project_id=os.getenv("GCP_PROJECT_ID"),
            region=os.getenv("GCP_REGION", "us-east1")
        )
        
        try:
            infra.setup_infrastructure_for_database(
                config_type=args.type
            )
            infra.get_infrastructure_status()
            
            logger.info("✅ Infrastructure setup completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Infrastructure setup failed: {e}")
            raise
    
    if args.update and args.type == "columns":
        infra = VectorSearchInfrastructure(
            project_id=os.getenv("GCP_PROJECT_ID"),
            region=os.getenv("GCP_REGION", "us-east1")
        )
        infra.update_column_embeddings()
        logger.info("✅ Infrastructure update completed successfully!")


if __name__ == "__main__":
    main()