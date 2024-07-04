// pages/another-page.tsx

import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';
import { InputWithButton1 } from '../components/InputWithButton1'
import { FeaturesGrid } from '../components/FeaturesGrid'
import {CommentSimple} from '../components/CommentSimple'


export default function AnotherPage() {
  return (
    <>
    <CommentSimple />
    <FeaturesGrid />
    <InputWithButton1 />
    <ColorSchemeToggle />
    
    </>
  );
}