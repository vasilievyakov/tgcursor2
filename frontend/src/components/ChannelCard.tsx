import React from 'react';
import { Channel } from '../services/api/index';
import { channelsApi } from '../services/api/index';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Avatar, AvatarImage, AvatarFallback } from './ui/avatar';
import { Trash2, RefreshCw, Eye } from 'lucide-react';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

interface ChannelCardProps {
  channel: Channel;
  onDelete?: () => void;
  onViewPosts?: () => void;
}

const ChannelCard: React.FC<ChannelCardProps> = ({ channel, onDelete, onViewPosts }) => {
  const handleParse = async () => {
    try {
      await channelsApi.parse(channel.id, channel.parse_mode);
    } catch (error) {
      console.error('Error triggering parse:', error);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Никогда';
    return format(new Date(dateString), 'dd MMM yyyy', { locale: ru });
  };

  return (
    <Card className="h-full flex flex-col hover:shadow-lg transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start gap-4">
          <Avatar className="h-16 w-16">
            <AvatarImage src={channel.channel_avatar_url} alt={channel.channel_name} />
            <AvatarFallback>{channel.channel_name.substring(0, 2).toUpperCase()}</AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <CardTitle className="text-lg truncate">{channel.channel_name}</CardTitle>
            <p className="text-sm text-muted-foreground mt-1">@{channel.channel_username}</p>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col">
        {channel.description && (
          <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
            {channel.description}
          </p>
        )}

        <div className="space-y-2 mb-4">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Подписчиков:</span>
            <span className="font-medium">{channel.subscribers_count.toLocaleString()}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Последний парсинг:</span>
            <span className="font-medium">{formatDate(channel.last_parsed_at)}</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          <Badge variant={channel.is_active ? 'default' : 'secondary'}>
            {channel.is_active ? 'Активен' : 'Неактивен'}
          </Badge>
          <Badge variant="outline">
            {channel.parse_mode === 'new_only' ? 'Только новые' : 'Полная история'}
          </Badge>
        </div>

        <div className="flex gap-2 mt-auto">
          <Button
            variant="outline"
            size="sm"
            onClick={handleParse}
            className="flex-1"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Парсить
          </Button>
          {onViewPosts && (
            <Button
              variant="outline"
              size="sm"
              onClick={onViewPosts}
              className="flex-1"
            >
              <Eye className="h-4 w-4 mr-2" />
              Посты
            </Button>
          )}
          {onDelete && (
            <Button
              variant="outline"
              size="sm"
              onClick={onDelete}
              className="text-destructive hover:text-destructive"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default ChannelCard;
