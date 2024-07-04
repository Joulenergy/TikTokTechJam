// pages/chat.tsx

import NavBar from '@/components/Navbar';
import { ChatInput } from '../components/ChatInput';
import { FeaturesGrid } from '../components/FeaturesGrid';
import { CommentSimple } from '../components/CommentSimple';

export default function AnotherPage() {
  return (
    <>
      <NavBar />
      <CommentSimple />
      <FeaturesGrid />
      <ChatInput />
    </>
  );
}
