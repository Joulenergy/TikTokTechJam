// import { Html, Head, Main, NextScript } from 'next/document';
// import { ColorSchemeScript } from '@mantine/core';

// export default function Document() {
//   return (
//     <Html lang="en">
//       <Head>
//         <ColorSchemeScript />
//       </Head>
//       <body>
//         <Main />
//         <NextScript />
//       </body>
//     </Html>
//   );
// }

import { Head, Html, Main, NextScript } from 'next/document';
import { ColorSchemeScript } from '@mantine/core';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <ColorSchemeScript defaultColorScheme="auto" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}