import type { ReactNode } from "react";

type AppLayoutProps = {
  children: ReactNode;
};

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="app-shell">
      <nav className="app-nav" aria-label="Primary">
        <p className="app-nav__title">Navigation Placeholder</p>
      </nav>
      <main className="app-main">{children}</main>
    </div>
  );
}
