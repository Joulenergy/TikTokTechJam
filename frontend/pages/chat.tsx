// pages/chat.tsx

import NavBar from '@/components/Navbar';
import { InputWithButton1 } from '../components/InputWithButton1';
import { FeaturesGrid } from '../components/FeaturesGrid';
import { CommentSimple } from '../components/CommentSimple';

export default function AnotherPage() {
  return (
    <>
      <NavBar />
      <CommentSimple />
      <FeaturesGrid />
      <InputWithButton1 />
    </>
  );
}
