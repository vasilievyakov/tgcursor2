import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { channelsApi, Channel, ChannelCreate } from '../../services/api/index';

interface ChannelsState {
  channels: Channel[];
  loading: boolean;
  error: string | null;
}

const initialState: ChannelsState = {
  channels: [],
  loading: false,
  error: null,
};

export const fetchChannels = createAsyncThunk(
  'channels/fetchChannels',
  async () => {
    const response = await channelsApi.list();
    return response.channels;
  }
);

export const createChannel = createAsyncThunk(
  'channels/createChannel',
  async (data: ChannelCreate) => {
    return await channelsApi.create(data);
  }
);

const channelsSlice = createSlice({
  name: 'channels',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchChannels.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchChannels.fulfilled, (state, action) => {
        state.loading = false;
        state.channels = action.payload;
      })
      .addCase(fetchChannels.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch channels';
      })
      .addCase(createChannel.fulfilled, (state, action) => {
        state.channels.push(action.payload);
      });
  },
});

export default channelsSlice.reducer;

