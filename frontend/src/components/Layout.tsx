interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <header role="banner" className="bg-gray-800 text-white py-4">
        <div className="mx-auto max-w-4xl px-4">
          <h1 className="text-xl font-bold">SDwC</h1>
        </div>
      </header>

      <main role="main" className="flex-1 mx-auto max-w-4xl w-full px-4 py-8">
        {children}
      </main>

      <footer role="contentinfo" className="bg-gray-100 py-4">
        <div className="mx-auto max-w-4xl px-4 text-center text-sm text-gray-600">
          <p>&copy; 2026 SDwC. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
