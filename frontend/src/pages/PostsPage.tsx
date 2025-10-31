import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { AppDispatch, RootState } from '../store';
import { fetchPosts, setPage, setPageSize } from '../store/slices/postsSlice';
import { fetchChannels } from '../store/slices/channelsSlice';
import PostsTable from '../components/PostsTable';
import Filters, { FilterState } from '../components/Filters';
import ExportDialog from '../components/ExportDialog';
import PostDetailDialog from '../components/PostDetailDialog';
import { Button } from '../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from '../components/ui/pagination';
import { Post } from '../services/api/index';
import { Download, FileText, AlertCircle, Loader2 } from 'lucide-react';

const PostsPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  
  const { posts, total, page, page_size, loading, error } = useSelector(
    (state: RootState) => state.posts
  );
  const { channels } = useSelector((state: RootState) => state.channels);
  
  const [filters, setFilters] = useState<FilterState>({
    channelId: searchParams.get('channel_id') ? parseInt(searchParams.get('channel_id')!) : undefined,
    sortBy: 'date',
    sortOrder: 'desc',
  });
  const [exportDialogOpen, setExportDialogOpen] = useState(false);
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);

  useEffect(() => {
    dispatch(fetchChannels());
  }, [dispatch]);

  useEffect(() => {
    loadPosts();
  }, [page, page_size, filters]);

  const loadPosts = () => {
    const params: any = {
      page,
      page_size,
    };

    if (filters.channelId) {
      params.channel_id = filters.channelId;
    }
    if (filters.contentType) {
      params.content_type = filters.contentType;
    }
    if (filters.dateFrom) {
      params.date_from = filters.dateFrom.toISOString();
    }
    if (filters.dateTo) {
      params.date_to = filters.dateTo.toISOString();
    }
    if (filters.keywords) {
      params.keywords = filters.keywords;
    }
    if (filters.search) {
      params.search = filters.search;
    }
    if (filters.sortBy) {
      params.sort_by = filters.sortBy;
    }
    if (filters.sortOrder) {
      params.sort_order = filters.sortOrder;
    }

    dispatch(fetchPosts(params));
  };

  const handleFilterChange = (newFilters: FilterState) => {
    setFilters(newFilters);
    dispatch(setPage(1));
  };

  const handlePageChange = (newPage: number) => {
    dispatch(setPage(newPage));
  };

  const handlePageSizeChange = (value: string) => {
    dispatch(setPageSize(parseInt(value)));
    dispatch(setPage(1));
  };

  const handleRowClick = (post: Post) => {
    setSelectedPost(post);
    setDetailDialogOpen(true);
  };

  const totalPages = Math.ceil(total / page_size);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Посты</h1>
          <p className="text-muted-foreground mt-1">
            Просмотр и анализ постов из Telegram каналов
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => navigate('/')}
          >
            <FileText className="mr-2 h-4 w-4" />
            Каналы
          </Button>
          <Button
            onClick={() => setExportDialogOpen(true)}
          >
            <Download className="mr-2 h-4 w-4" />
            Экспорт
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Filters
        onFilterChange={handleFilterChange}
        channels={channels.map(ch => ({ id: ch.id, channel_name: ch.channel_name }))}
      />

      {/* Error */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>Ошибка: {error}</AlertDescription>
        </Alert>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      )}

      {/* Content */}
      {!loading && (
        <>
          <div className="flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              Всего постов: <span className="font-medium">{total}</span>
            </p>
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">Строк на странице:</span>
              <Select value={page_size.toString()} onValueChange={handlePageSizeChange}>
                <SelectTrigger className="w-[100px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="25">25</SelectItem>
                  <SelectItem value="50">50</SelectItem>
                  <SelectItem value="100">100</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <PostsTable posts={posts} loading={loading} onRowClick={handleRowClick} />

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center">
              <Pagination>
                <PaginationContent>
                  <PaginationItem>
                    <PaginationPrevious
                      onClick={() => handlePageChange(Math.max(1, page - 1))}
                      className={page === 1 ? 'pointer-events-none opacity-50' : 'cursor-pointer'}
                    />
                  </PaginationItem>
                  
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    let pageNum;
                    if (totalPages <= 5) {
                      pageNum = i + 1;
                    } else if (page <= 3) {
                      pageNum = i + 1;
                    } else if (page >= totalPages - 2) {
                      pageNum = totalPages - 4 + i;
                    } else {
                      pageNum = page - 2 + i;
                    }
                    
                    return (
                      <PaginationItem key={pageNum}>
                        <PaginationLink
                          onClick={() => handlePageChange(pageNum)}
                          isActive={page === pageNum}
                          className="cursor-pointer"
                        >
                          {pageNum}
                        </PaginationLink>
                      </PaginationItem>
                    );
                  })}
                  
                  <PaginationItem>
                    <PaginationNext
                      onClick={() => handlePageChange(Math.min(totalPages, page + 1))}
                      className={page === totalPages ? 'pointer-events-none opacity-50' : 'cursor-pointer'}
                    />
                  </PaginationItem>
                </PaginationContent>
              </Pagination>
            </div>
          )}
        </>
      )}

      {/* Dialogs */}
      <ExportDialog
        open={exportDialogOpen}
        onClose={() => setExportDialogOpen(false)}
        filters={filters}
      />

      <PostDetailDialog
        post={selectedPost}
        open={detailDialogOpen}
        onClose={() => setDetailDialogOpen(false)}
      />
    </div>
  );
};

export default PostsPage;
