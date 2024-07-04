import React from 'react';
import { TextInput, TextInputProps, ActionIcon, useMantineTheme, rem } from '@mantine/core';
import { IconArrowRight } from '@tabler/icons-react';
import { useState } from 'react';

export function ChatInput(props: TextInputProps) {
  const theme = useMantineTheme();
  const [value, setValue] = useState('');

  const exists = localStorage.getItem('messages');
  const messages = exists ? JSON.parse(exists) : [];
  const sendMessage = async () => {
    if (value.length > 100) {
      alert('Must not exceed 100 characters');
    } else {
      messages.push(value)
      localStorage.setItem('messages', JSON.stringify(messages))
      setValue('');
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column', // Align items in a column
        justifyContent: 'flex-end',
        // height: '85vh', // This makes the div take up the full viewport height
        padding: '10px',
      }}
    >
      {/* <div style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Image radius="md" h={80} w={80} component={NextImage} src={logo} alt="My Logo" />
        </div>
      </div> */}
      <p style={{ textAlign: 'left' }}>What would you like to explore about these videos?</p>
      <div style={{ marginBottom: '1rem' }}>
        <TextInput
          radius="xl"
          size="md"
          placeholder="Message CommentSense!"
          value={value}
          onChange={(event) => setValue(event.currentTarget.value)}
          rightSectionWidth={42}
          rightSection={
            <ActionIcon
              size={32}
              radius="xl"
              color={theme.primaryColor}
              variant="filled"
              onClick={sendMessage} // Add onClick handler to navigate to another page
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

export default ChatInput;
