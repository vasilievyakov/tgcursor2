import { configureStore } from '@reduxjs/toolkit';
import channelsReducer from './slices/channelsSlice';
import postsReducer from './slices/postsSlice';

export const store = configureStore({
  reducer: {
    channels: channelsReducer,
    posts: postsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

