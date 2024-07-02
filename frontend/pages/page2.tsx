// pages/another-page.tsx

import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';
import { InputWithButton1 } from '../components/InputWithButton1'
import { FeaturesGrid } from '../components/FeaturesGrid'



export default function AnotherPage() {
  return (
    <>
    <InputWithButton1 />
    {/* <FeaturesGrid /> */}
    <ColorSchemeToggle />
    
    </>
  );
}