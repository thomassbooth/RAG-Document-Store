import React from 'react';
import Link from 'next/link';

const Navbar = () => {
  return (
    <nav className="py-4">
      <div className="container mx-auto flex justify-between">
        <div className="text-white text-lg font-bold">
          Open Innovations AI
        </div>
        <div className="flex space-x-4">
          <Link href="/" className="text-white hover:opacity-80">
            Home
          </Link>
          <Link href="/upload" className="text-white hover:opacity-80">
            Upload
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
