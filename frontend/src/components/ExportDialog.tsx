import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from './ui/dialog';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Label } from './ui/label';
import { Alert, AlertDescription } from './ui/alert';
import { exportApi } from '../services/api/index';
import { FilterState } from './Filters';
import { Loader2, AlertCircle, Download } from 'lucide-react';

interface ExportDialogProps {
  open: boolean;
  onClose: () => void;
  filters: FilterState;
}

const ExportDialog: React.FC<ExportDialogProps> = ({ open, onClose, filters }) => {
  const [format, setFormat] = useState<'csv' | 'excel'>('csv');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExport = async () => {
    setLoading(true);
    setError(null);

    try {
      const params: any = {};
      
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

      const blob = await exportApi.exportPosts(format, params);

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `posts_export_${new Date().toISOString().split('T')[0]}.${format === 'csv' ? 'csv' : 'xlsx'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      onClose();
    } catch (err: any) {
      setError(err.message || 'Ошибка при экспорте данных');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Экспорт данных</DialogTitle>
          <DialogDescription>
            Выберите формат для экспорта отфильтрованных постов
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="export-format">Формат экспорта</Label>
            <Select value={format} onValueChange={(v) => setFormat(v as 'csv' | 'excel')}>
              <SelectTrigger id="export-format">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="csv">CSV</SelectItem>
                <SelectItem value="excel">Excel (.xlsx)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={loading}>
            Отмена
          </Button>
          <Button onClick={handleExport} disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Экспорт...
              </>
            ) : (
              <>
                <Download className="mr-2 h-4 w-4" />
                Экспортировать
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ExportDialog;
