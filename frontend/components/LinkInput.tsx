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
    // TODO: send post request with value
    router.push('./chat');
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
