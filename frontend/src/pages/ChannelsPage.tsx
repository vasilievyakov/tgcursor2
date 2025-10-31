import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { AppDispatch, RootState } from '../store';
import { fetchChannels } from '../store/slices/channelsSlice';
import AddChannelForm from '../components/AddChannelForm';
import ChannelCard from '../components/ChannelCard';
import { Button } from '../components/ui/button';
import { Skeleton } from '../components/ui/skeleton';
import { Alert, AlertDescription } from '../components/ui/alert';
import { channelsApi } from '../services/api/index';
import { Plus, MessageSquare, AlertCircle, FileText } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';

const ChannelsPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { channels, loading, error } = useSelector((state: RootState) => state.channels);
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    dispatch(fetchChannels());
  }, [dispatch]);

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот канал?')) {
      try {
        await channelsApi.delete(id);
        dispatch(fetchChannels());
      } catch (error) {
        console.error('Error deleting channel:', error);
      }
    }
  };

  const handleViewPosts = (channelId: number) => {
    navigate(`/posts?channel_id=${channelId}`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Telegram каналы</h1>
          <p className="text-muted-foreground mt-1">
            Управляйте каналами для парсинга контента
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => navigate('/posts')}
          >
            <FileText className="mr-2 h-4 w-4" />
            Все посты
          </Button>
          <Button
            onClick={() => setShowAddForm(!showAddForm)}
          >
            <Plus className="mr-2 h-4 w-4" />
            {showAddForm ? 'Скрыть форму' : 'Добавить канал'}
          </Button>
        </div>
      </div>

      {/* Add Form */}
      {showAddForm && (
        <div className="mb-6">
          <AddChannelForm />
        </div>
      )}

      {/* Error */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>Ошибка: {error}</AlertDescription>
        </Alert>
      )}

      {/* Loading */}
      {loading && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <Card key={i}>
              <CardContent className="p-6">
                <div className="space-y-3">
                  <Skeleton className="h-16 w-16 rounded-full" />
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                  <div className="flex gap-2">
                    <Skeleton className="h-8 flex-1" />
                    <Skeleton className="h-8 flex-1" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && channels.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <MessageSquare className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Нет добавленных каналов</h3>
            <p className="text-muted-foreground text-center mb-4">
              Добавьте первый канал, чтобы начать парсинг
            </p>
            <Button onClick={() => setShowAddForm(true)}>
              <Plus className="mr-2 h-4 w-4" />
              Добавить канал
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Channels Grid */}
      {!loading && channels.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {channels.map((channel) => (
            <ChannelCard
              key={channel.id}
              channel={channel}
              onDelete={() => handleDelete(channel.id)}
              onViewPosts={() => handleViewPosts(channel.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default ChannelsPage;
