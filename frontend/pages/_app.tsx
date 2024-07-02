// import '@mantine/core/styles.css';
// import type { AppProps } from 'next/app';
// import Head from 'next/head';
// import { MantineProvider } from '@mantine/core';
// import { theme } from '../theme';

// export default function App({ Component, pageProps }: AppProps) {
//   return (
//     <MantineProvider theme={theme}>
//       <Head>
//         <title>Mantine Template</title>
//         <meta
//           name="viewport"
//           content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
//         />
//         <link rel="shortcut icon" href="/favicon.svg" />
//       </Head>
//       <Component {...pageProps} />
//     </MantineProvider>
//   );
// }

// Import styles of packages that you've installed.
// All packages except `@mantine/hooks` require styles imports
import '@mantine/core/styles.css';

import type { AppProps } from 'next/app';
import { MantineProvider } from '@mantine/core';


export default function App({ Component, pageProps }: AppProps) {
  return (
    <MantineProvider>
      <Component {...pageProps} />
    </MantineProvider>
  );
}