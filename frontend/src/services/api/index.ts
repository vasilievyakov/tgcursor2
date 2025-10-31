import apiClient from '../api';

export interface Channel {
  id: number;
  channel_username: string;
  channel_name: string;
  channel_avatar_url?: string;
  subscribers_count: number;
  description?: string;
  is_active: boolean;
  parse_mode: string;
  last_parsed_at?: string;
  created_at: string;
}

export interface Post {
  id: number;
  post_id: string;
  channel_id: number;
  date: string;
  text?: string;
  author?: string;
  views: number;
  likes: number;
  engagement_rate?: number;
  content_type: string;
  media_urls?: string[];
  hashtags?: string[];
  mentions?: string[];
  links?: string[];
}

export interface ChannelCreate {
  channel_username: string;
  channel_name: string;
  parse_mode: 'new_only' | 'full_history';
}

export interface PostListResponse {
  posts: Post[];
  total: number;
  page: number;
  page_size: number;
}

export interface ChannelListResponse {
  channels: Channel[];
  total: number;
}

export const channelsApi = {
  list: async (): Promise<ChannelListResponse> => {
    const response = await apiClient.get('/channels/');
    return response.data;
  },
  
  get: async (id: number): Promise<Channel> => {
    const response = await apiClient.get(`/channels/${id}`);
    return response.data;
  },
  
  create: async (data: ChannelCreate): Promise<Channel> => {
    const response = await apiClient.post('/channels/', data);
    return response.data;
  },
  
  update: async (id: number, data: Partial<Channel>): Promise<Channel> => {
    const response = await apiClient.patch(`/channels/${id}`, data);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/channels/${id}`);
  },
  
  parse: async (id: number, parse_mode: string = 'new_only'): Promise<void> => {
    await apiClient.post(`/channels/${id}/parse`, null, {
      params: { parse_mode },
    });
  },
};

export const postsApi = {
  list: async (params?: {
    page?: number;
    page_size?: number;
    channel_id?: number;
    content_type?: string;
    date_from?: string;
    date_to?: string;
    keywords?: string;
    search?: string;
    sort_by?: string;
    sort_order?: string;
  }): Promise<PostListResponse> => {
    const response = await apiClient.get('/posts/', { params });
    return response.data;
  },
  
  get: async (id: number): Promise<Post> => {
    const response = await apiClient.get(`/posts/${id}`);
    return response.data;
  },
};

export const exportApi = {
  exportPosts: async (
    format: 'csv' | 'excel',
    params?: {
      channel_id?: number;
      content_type?: string;
      date_from?: string;
      date_to?: string;
      keywords?: string;
      search?: string;
      columns?: string;
    }
  ): Promise<Blob> => {
    const response = await apiClient.post('/export/posts', null, {
      params: { export_format: format, ...params },
      responseType: 'blob',
    });
    return response.data;
  },
};

