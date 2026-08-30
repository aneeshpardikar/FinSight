import "./globals.css";

export const metadata = {
  title: "Stockflow | Investment dashboard",
  description: "A personal investment dashboard for Indian stocks.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
