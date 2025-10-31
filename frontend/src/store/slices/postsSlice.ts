import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { postsApi, Post, PostListResponse } from '../../services/api/index';

interface PostsState {
  posts: Post[];
  total: number;
  page: number;
  page_size: number;
  loading: boolean;
  error: string | null;
}

const initialState: PostsState = {
  posts: [],
  total: 0,
  page: 1,
  page_size: 50,
  loading: false,
  error: null,
};

export const fetchPosts = createAsyncThunk(
  'posts/fetchPosts',
  async (params?: {
    page?: number;
    page_size?: number;
    channel_id?: number;
    content_type?: string;
    search?: string;
    sort_by?: string;
    sort_order?: string;
  }) => {
    const response = await postsApi.list(params);
    return response;
  }
);

const postsSlice = createSlice({
  name: 'posts',
  initialState,
  reducers: {
    setPage: (state, action: PayloadAction<number>) => {
      state.page = action.payload;
    },
    setPageSize: (state, action: PayloadAction<number>) => {
      state.page_size = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchPosts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.loading = false;
        state.posts = action.payload.posts;
        state.total = action.payload.total;
        state.page = action.payload.page;
        state.page_size = action.payload.page_size;
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch posts';
      });
  },
});

export const { setPage, setPageSize } = postsSlice.actions;
export default postsSlice.reducer;

