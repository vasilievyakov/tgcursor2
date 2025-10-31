import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { createChannel } from '../store/slices/channelsSlice';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsList, TabsTrigger } from './ui/tabs';
import { Alert, AlertDescription } from './ui/alert';
import { Loader2, Plus, CheckCircle2, AlertCircle } from 'lucide-react';

const AddChannelForm: React.FC = () => {
  const dispatch = useDispatch();
  const [channelUrl, setChannelUrl] = useState('');
  const [parseMode, setParseMode] = useState<'new_only' | 'full_history'>('new_only');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const extractUsername = (url: string): string => {
    if (url.startsWith('https://t.me/')) {
      return url.replace('https://t.me/', '').replace('@', '');
    }
    if (url.startsWith('@')) {
      return url.replace('@', '');
    }
    return url;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const username = extractUsername(channelUrl);
      if (!username) {
        throw new Error('Введите корректную ссылку на канал');
      }

      await dispatch(createChannel({
        channel_username: username,
        channel_name: username,
        parse_mode: parseMode,
      }) as any).unwrap();

      setSuccess(true);
      setChannelUrl('');
      
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.message || 'Ошибка при добавлении канала');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Добавить канал</CardTitle>
        <CardDescription>
          Введите ссылку на Telegram канал для начала парсинга
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="channel-url">Ссылка на канал</Label>
            <Input
              id="channel-url"
              placeholder="https://t.me/channelname или @channelname"
              value={channelUrl}
              onChange={(e) => setChannelUrl(e.target.value)}
              disabled={loading}
              required
            />
          </div>

          <div className="space-y-2">
            <Label>Режим парсинга</Label>
            <Tabs value={parseMode} onValueChange={(v) => setParseMode(v as 'new_only' | 'full_history')}>
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="new_only">Только новые</TabsTrigger>
                <TabsTrigger value="full_history">Полная история</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert className="border-green-500 bg-green-50 text-green-900">
              <CheckCircle2 className="h-4 w-4" />
              <AlertDescription>Канал успешно добавлен! Парсинг начат.</AlertDescription>
            </Alert>
          )}

          <Button
            type="submit"
            disabled={loading || !channelUrl}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Добавление...
              </>
            ) : (
              <>
                <Plus className="mr-2 h-4 w-4" />
                Добавить канал
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default AddChannelForm;
