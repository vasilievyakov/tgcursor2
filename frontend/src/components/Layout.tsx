import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MessageSquare, BarChart3 } from 'lucide-react';
import { Button } from './ui/button';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();

  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-6">
            <Link to="/" className="flex items-center gap-2">
              <MessageSquare className="h-6 w-6 text-primary" />
              <span className="text-xl font-bold">Telegram Parser</span>
            </Link>
          </div>
          
          <nav className="flex items-center gap-2">
            <Button
              variant={location.pathname === '/' ? 'default' : 'ghost'}
              asChild
            >
              <Link to="/" className="flex items-center gap-2">
                <BarChart3 className="h-4 w-4" />
                Каналы
              </Link>
            </Button>
            <Button
              variant={location.pathname.startsWith('/posts') ? 'default' : 'ghost'}
              asChild
            >
              <Link to="/posts" className="flex items-center gap-2">
                <MessageSquare className="h-4 w-4" />
                Посты
              </Link>
            </Button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 container py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t bg-muted/50 py-6 mt-auto">
        <div className="container flex flex-col items-center justify-between gap-4 md:flex-row">
          <p className="text-sm text-muted-foreground">
            Telegram Content Parser & Analyzer MVP
          </p>
          <p className="text-sm text-muted-foreground">
            © 2024 All rights reserved
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
