from typing import List, Dict, Any

class AISStreamIngestion:
    """
    Ingests live AIS vessel contacts from aisstream.io WebSocket stream
    for the Arabian Sea, Bay of Bengal, Hormuz, and Malacca.
    """
    def __init__(self):
        pass

    def get_monitoring_bounding_boxes(self):
        return [
            {"name": "Arabian Sea", "bbox": [[10.0, 55.0], [26.0, 76.0]]},
            {"name": "Bay of Bengal", "bbox": [[5.0, 79.0], [22.5, 96.0]]},
            {"name": "Strait of Hormuz", "bbox": [[25.0, 54.8], [27.5, 57.2]]},
            {"name": "Strait of Malacca", "bbox": [[1.0, 95.0], [6.0, 104.0]]}
        ]

aisstream_ingestion = AISStreamIngestion()
