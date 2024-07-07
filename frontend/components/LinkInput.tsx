import React, { useState } from 'react';
import { ActionIcon, useMantineTheme, rem, Image, TagsInput } from '@mantine/core';
import { IconSearch, IconArrowRight } from '@tabler/icons-react';
import logo from '../public/logo.png';
import NextImage from 'next/image';
import { useRouter } from 'next/router';

export function LinkInput() {
  const theme = useMantineTheme();
  const router = useRouter();
  const [value, setValue] = useState<string[]>([]);

  const handleButtonClick = () => {
    // Navigate to the desired page here

    // Check if the link is in the valid format
    if (value.length === 0) {
      alert('Please enter a valid link!');
      return;
    }

    const endpoint = 'http://localhost:8000/summarize/';

    // call the API
    fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        URLS: value,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
        // Get the first key insdie data['results']
        const url = Object.keys(data['results'])[0];
        localStorage.setItem('context', url);
        router.push('./chat');
      })
      .catch((error) => {
        console.error('Error:', error);
        alert('There was an error processing your request. Please try again later.');
      });

    
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        padding: '10px',
      }}
    >
      <div style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Image radius="md" h={80} w={80} component={NextImage} src={logo} alt="My Logo" />
        </div>
      </div>
      <p style={{ textAlign: 'center' }}>What would you like me to analyse today?</p>
      <div style={{ marginBottom: '1rem' }}>
        <TagsInput
          styles={(theme) => ({
            input: {
              borderRadius: theme.radius.md,
            },
          })}
          size="md"
          placeholder="Paste up to 3 links here!"
          maxTags={3}
          value={value} 
          onChange={setValue}
          leftSection={<IconSearch style={{ width: rem(18), height: rem(18) }} stroke={1.5} />}
          rightSection={
            <ActionIcon
              size={32}
              radius="xl"
              color={theme.primaryColor}
              variant="filled"
              onClick={handleButtonClick}
              style={{ cursor: 'pointer' }}
            >
              <IconArrowRight style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
            </ActionIcon>
          }
        />
      </div>
    </div>
  );
}

export default LinkInput;