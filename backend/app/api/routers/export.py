"""
API routers for export.
"""
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.core.database import get_db
from app.agents.filter_search import FilterSearchAgent
from app.agents.export import ExportAgent
from app.core.config import settings

router = APIRouter(prefix="/export", tags=["export"])


@router.post("/posts")
async def export_posts(
    export_format: str = Query("csv", regex="^(csv|excel)$"),
    channel_id: Optional[int] = None,
    content_type: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    keywords: Optional[str] = None,
    search: Optional[str] = None,
    columns: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export posts in specified format."""
    # Build filters
    filters = {}
    
    if channel_id:
        filters["channel_ids"] = [channel_id]
    
    if content_type:
        filters["content_types"] = [content_type]
    
    if date_from:
        filters["date_from"] = date_from
    
    if date_to:
        filters["date_to"] = date_to
    
    if keywords:
        filters["keywords"] = keywords.split(",")
    
    # Get posts
    agent = FilterSearchAgent(db)
    result = agent.get_filtered_posts(
        filters=filters if filters else None,
        search_query=search,
        sort_by="date",
        sort_order="desc",
        page=1,
        page_size=settings.MAX_EXPORT_ROWS
    )
    
    # Check limit
    if result["total"] > settings.MAX_EXPORT_ROWS:
        raise HTTPException(
            status_code=400,
            detail=f"Export limit exceeded. Maximum {settings.MAX_EXPORT_ROWS} rows allowed."
        )
    
    # Prepare posts for export
    exporter = ExportAgent()
    export_data = exporter.prepare_posts_for_export(result["posts"])
    
    # Parse columns if provided
    export_columns = None
    if columns:
        export_columns = [col.strip() for col in columns.split(",")]
    
    # Export
    if export_format == "csv":
        file_bytes = exporter.export_to_csv(export_data, columns=export_columns)
        media_type = "text/csv"
        filename = f"posts_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    elif export_format == "excel":
        file_bytes = exporter.export_to_excel(export_data, columns=export_columns)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"posts_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.xlsx"
    else:
        raise HTTPException(status_code=400, detail="Invalid export format")
    
    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

