```markdown
# FPS Game Performance Analyzer

An intelligent application that analyzes FPS game performance using computer vision to track player accuracy and movement patterns. The system processes game screenshots in real-time through Detectron2's object detection model to calculate crosshair-to-target distances.

Built with Python/Flask backend exposed via ngrok for remote processing, with data persistence handled through PostgreSQL. The desktop client captures and transmits gameplay screenshots, receiving instant feedback on aim precision and tracking statistics over time.

## Technologies Used
- Python/Flask for backend server
- Detectron2 for computer vision and object detection 
- PostgreSQL/SQLite3 for data persistence
- ngrok for server exposure
