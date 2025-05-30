#!/usr/bin/env python3
"""
Basic usage example for Cloud Splitter
"""
import asyncio
from pathlib import Path
from cloud_splitter.core.workflow import ProcessingWorkflow
from cloud_splitter.core.config_loader import ConfigLoader
from cloud_splitter.utils.logging import setup_logging

async def main():
    # Set up logging
    logger = setup_logging()
    
    # Load configuration
    config = ConfigLoader.load_config()
    
    # Create workflow
    workflow = ProcessingWorkflow(config)
    
    # Add URLs to process
    urls = [
        "https://www.youtube.com/watch?v=example1",
        "https://www.youtube.com/watch?v=example2"
    ]
    
    try:
        # Add URLs to queue
        items = await workflow.add_urls(urls)
        logger.info(f"Added {len(items)} URLs to queue")
        
        # Process queue
        results = await workflow.process_queue()
        
        # Print results
        for result in results:
            print(f"\nProcessed: {result['url']}")
            print(f"Title: {result['title']}")
            print(f"Artist: {result['artist']}")
            print("Stems:")
            for stem_name, stem_path in result['stems'].items():
                print(f"  - {stem_name}: {stem_path}")
            
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
