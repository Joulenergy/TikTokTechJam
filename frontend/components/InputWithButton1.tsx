import React from 'react';
import { TextInput, TextInputProps, ActionIcon, useMantineTheme, rem, Image } from '@mantine/core';
import { IconSearch, IconArrowRight } from '@tabler/icons-react';
import { useRouter } from 'next/router'; // Import useRouter hook from Next.js

export function InputWithButton1(props: TextInputProps) {
  const theme = useMantineTheme();
  const router = useRouter();

  const handleButtonClick = () => {
    // Navigate to the desired page here
    router.push('./chat');
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column', // Align items in a column
        justifyContent: 'flex-end',
        // height: '85vh', // This makes the div take up the full viewport height
        // padding: '10px'
      }}
    >
      {/* <div style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Image radius="md" h={80} w={80} component={NextImage} src={logo} alt="My Logo" />
        </div>
      </div> */}
      <p style={{ textAlign: 'left' }}>What would you like me to analyse today?</p>
      <div style={{ marginBottom: '1rem' }}>
        <TextInput
          radius="xl"
          size="md"
          placeholder="Message CommentSense!"
          rightSectionWidth={42}
          leftSection={<IconSearch style={{ width: rem(18), height: rem(18) }} stroke={1.5} />}
          rightSection={
            <ActionIcon
              size={32}
              radius="xl"
              color={theme.primaryColor}
              variant="filled"
              onClick={handleButtonClick} // Add onClick handler to navigate to another page
              style={{ cursor: 'pointer' }} // Optional: Show pointer cursor on hover
            >
              <IconArrowRight style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
            </ActionIcon>
          }
          {...props}
        />
      </div>
    </div>
  );
}

export default InputWithButton1;
