import React, { useState } from 'react';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Separator } from './ui/separator';
import { Search, Filter, X } from 'lucide-react';

interface FiltersProps {
  onFilterChange: (filters: FilterState) => void;
  channels?: Array<{ id: number; channel_name: string }>;
}

export interface FilterState {
  channelId?: number;
  contentType?: string;
  dateFrom?: Date | null;
  dateTo?: Date | null;
  keywords?: string;
  search?: string;
  sortBy?: string;
  sortOrder?: string;
}

const Filters: React.FC<FiltersProps> = ({ onFilterChange, channels = [] }) => {
  const [filters, setFilters] = useState<FilterState>({
    sortBy: 'date',
    sortOrder: 'desc',
  });
  const [isExpanded, setIsExpanded] = useState(false);

  const handleFilterChange = (key: keyof FilterState, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleReset = () => {
    const resetFilters: FilterState = {
      sortBy: 'date',
      sortOrder: 'desc',
    };
    setFilters(resetFilters);
    onFilterChange(resetFilters);
  };

  const hasActiveFilters = Boolean(
    filters.channelId || filters.contentType || filters.dateFrom || filters.dateTo || filters.keywords
  );

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-lg">Фильтры и поиск</CardTitle>
            <CardDescription>Настройте параметры фильтрации и сортировки</CardDescription>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            <Filter className="h-4 w-4 mr-2" />
            {isExpanded ? 'Скрыть' : 'Показать'}
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Search */}
        <div className="space-y-2">
          <Label htmlFor="search">Поиск</Label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              id="search"
              placeholder="Введите текст для поиска..."
              value={filters.search || ''}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {isExpanded && (
          <>
            <Separator />
            
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {/* Keywords */}
              <div className="space-y-2">
                <Label htmlFor="keywords">Ключевые слова</Label>
                <Input
                  id="keywords"
                  placeholder="word1, word2, word3"
                  value={filters.keywords || ''}
                  onChange={(e) => handleFilterChange('keywords', e.target.value)}
                />
              </div>

              {/* Channel */}
              <div className="space-y-2">
                <Label htmlFor="channel">Канал</Label>
                <Select
                  value={filters.channelId?.toString() || ''}
                  onValueChange={(value) => handleFilterChange('channelId', value ? parseInt(value) : undefined)}
                >
                  <SelectTrigger id="channel">
                    <SelectValue placeholder="Все каналы" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">Все каналы</SelectItem>
                    {channels.map((channel) => (
                      <SelectItem key={channel.id} value={channel.id.toString()}>
                        {channel.channel_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Content Type */}
              <div className="space-y-2">
                <Label htmlFor="content-type">Тип контента</Label>
                <Select
                  value={filters.contentType || ''}
                  onValueChange={(value) => handleFilterChange('contentType', value || undefined)}
                >
                  <SelectTrigger id="content-type">
                    <SelectValue placeholder="Все типы" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">Все типы</SelectItem>
                    <SelectItem value="text">Текст</SelectItem>
                    <SelectItem value="photo">Фото</SelectItem>
                    <SelectItem value="video">Видео</SelectItem>
                    <SelectItem value="document">Документ</SelectItem>
                    <SelectItem value="link">Ссылка</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Sort By */}
              <div className="space-y-2">
                <Label htmlFor="sort-by">Сортировка</Label>
                <Select
                  value={filters.sortBy || 'date'}
                  onValueChange={(value) => handleFilterChange('sortBy', value)}
                >
                  <SelectTrigger id="sort-by">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="date">Дата</SelectItem>
                    <SelectItem value="views">Просмотры</SelectItem>
                    <SelectItem value="likes">Лайки</SelectItem>
                    <SelectItem value="engagement_rate">Engagement</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Sort Order */}
              <div className="space-y-2">
                <Label htmlFor="sort-order">Порядок</Label>
                <Select
                  value={filters.sortOrder || 'desc'}
                  onValueChange={(value) => handleFilterChange('sortOrder', value)}
                >
                  <SelectTrigger id="sort-order">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="desc">По убыванию</SelectItem>
                    <SelectItem value="asc">По возрастанию</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {hasActiveFilters && (
              <div className="flex justify-end">
                <Button variant="outline" onClick={handleReset}>
                  <X className="h-4 w-4 mr-2" />
                  Сбросить фильтры
                </Button>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default Filters;
