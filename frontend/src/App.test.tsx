import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders welcome message', () => {
    render(<App />);
    const heading = screen.getByText(/Telegram Content Parser & Analyzer/i);
    expect(heading).toBeInTheDocument();
  });
});

