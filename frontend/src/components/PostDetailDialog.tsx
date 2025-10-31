import React from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from './ui/dialog';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { Post } from '../services/api/index';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import { ExternalLink, Eye, Heart, TrendingUp, Hash, AtSign, Link as LinkIcon, Image } from 'lucide-react';

interface PostDetailDialogProps {
  post: Post | null;
  open: boolean;
  onClose: () => void;
}

const PostDetailDialog: React.FC<PostDetailDialogProps> = ({ post, open, onClose }) => {
  if (!post) return null;

  const formatDate = (dateString: string) => {
    return format(new Date(dateString), 'dd MMM yyyy HH:mm', { locale: ru });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Детали поста</DialogTitle>
          <DialogDescription>
            Подробная информация о посте
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Meta Info */}
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">
                ID поста: <span className="font-medium">{post.post_id}</span>
              </p>
              <p className="text-sm text-muted-foreground">
                Дата: <span className="font-medium">{formatDate(post.date)}</span>
              </p>
            </div>
            <Badge variant="outline" className="text-sm">
              {post.content_type}
            </Badge>
          </div>

          <Separator />

          {/* Text */}
          {post.text && (
            <div className="space-y-2">
              <h4 className="text-sm font-semibold">Текст:</h4>
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{post.text}</p>
            </div>
          )}

          {/* Author */}
          {post.author && (
            <div className="space-y-2">
              <h4 className="text-sm font-semibold">Автор:</h4>
              <p className="text-sm">{post.author}</p>
            </div>
          )}

          {/* Metrics */}
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">Метрики:</h4>
            <div className="flex flex-wrap gap-4">
              <div className="flex items-center gap-2">
                <Eye className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">
                  Просмотры: <span className="font-medium">{post.views.toLocaleString()}</span>
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Heart className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">
                  Лайки: <span className="font-medium">{post.likes.toLocaleString()}</span>
                </span>
              </div>
              {post.engagement_rate && (
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">
                    Engagement: <span className="font-medium">{(post.engagement_rate * 100).toFixed(2)}%</span>
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Hashtags */}
          {post.hashtags && post.hashtags.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-semibold flex items-center gap-2">
                <Hash className="h-4 w-4" />
                Хештеги:
              </h4>
              <div className="flex flex-wrap gap-2">
                {post.hashtags.map((tag: string, index: number) => (
                  <Badge key={index} variant="secondary">
                    {tag}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Mentions */}
          {post.mentions && post.mentions.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-semibold flex items-center gap-2">
                <AtSign className="h-4 w-4" />
                Упоминания:
              </h4>
              <div className="flex flex-wrap gap-2">
                {post.mentions.map((mention: string, index: number) => (
                  <Badge key={index} variant="outline">
                    {mention}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Links */}
          {post.links && post.links.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-semibold flex items-center gap-2">
                <LinkIcon className="h-4 w-4" />
                Ссылки:
              </h4>
              <div className="space-y-1">
                {post.links.map((link: string, index: number) => (
                  <a
                    key={index}
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-primary hover:underline flex items-center gap-1 break-all"
                  >
                    {link}
                    <ExternalLink className="h-3 w-3" />
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Media */}
          {post.media_urls && post.media_urls.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-semibold flex items-center gap-2">
                <Image className="h-4 w-4" />
                Медиа:
              </h4>
              <div className="space-y-1">
                {post.media_urls.map((url: string, index: number) => (
                  <a
                    key={index}
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-primary hover:underline flex items-center gap-1 break-all"
                  >
                    {url}
                    <ExternalLink className="h-3 w-3" />
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>

        <DialogFooter>
          <Button onClick={onClose}>Закрыть</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default PostDetailDialog;
