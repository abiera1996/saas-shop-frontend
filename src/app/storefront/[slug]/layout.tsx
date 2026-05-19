import { CustomerAuthProvider } from "./CustomerAuthProvider";
import { StorefrontNavbar } from "./StorefrontNavbar";

export default async function StorefrontLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return (
    <CustomerAuthProvider shopSlug={slug}>
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <StorefrontNavbar shopSlug={slug} />
        <main className="flex-1">
          {children}
        </main>
      </div>
    </CustomerAuthProvider>
  );
}
