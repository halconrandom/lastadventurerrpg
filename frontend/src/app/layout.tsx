import type { Metadata, Viewport } from "next";
import { Cinzel, Lora } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const cinzel = Cinzel({
  subsets: ["latin"],
  variable: "--font-cinzel",
  display: "swap",
});

const lora = Lora({
  subsets: ["latin"],
  variable: "--font-lora",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Last Adventurer | RPG de Mundo Abierto",
  description: "Un RPG basado en texto con un vasto mundo abierto lleno de aventuras, misterios y combates épicos",
};

export const viewport: Viewport = {
  themeColor: "#1a1a2e",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="dark">
      <body className={`${cinzel.variable} ${lora.variable} font-serif antialiased`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}