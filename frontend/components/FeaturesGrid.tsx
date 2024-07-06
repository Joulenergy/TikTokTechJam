import { useMantineColorScheme, ThemeIcon, Text, Container, SimpleGrid, rem } from '@mantine/core';
import { IconMessage, IconBulb, IconMoodSearch } from '@tabler/icons-react';
import { Dispatch, SetStateAction } from 'react';

export const prompts = [
  {
    icon: IconMessage,
    title: 'summarise video comments',
  },
  {
    icon: IconMoodSearch,
    title: 'conduct sentiment analysis',
  },
  {
    icon: IconBulb,
    title: 'suggest new ideas for future videos',
  },
];

interface FeatureProps {
  icon: React.FC<any>;
  title: string;
  setValue: Dispatch<SetStateAction<string>>;
  goBot: () => void;
}

function Feature({ icon: Icon, title, setValue, goBot }: FeatureProps) {
  const { colorScheme } = useMantineColorScheme();
  const changeChatInput = (prompt: string) => {
    setValue(prompt);
    goBot();
  };
  return (
    <div
      style={{
        background: colorScheme === 'dark' ? '#2C2E33' : '#f0f0f0',
        border: `1px solid ${colorScheme === 'dark' ? '#4A4A4A' : '#e0e0e0'}`,
        padding: '10px',
        borderRadius: '10px',
        display: 'inline-block',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease',
      }}
      onClick={() => {
        changeChatInput(title);
      }}
    >
      <ThemeIcon variant="light" size={40} radius={40}>
        <Icon style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
      </ThemeIcon>
      <Text mt="sm" mb={7}>
        {title}
      </Text>
    </div>
  );
}

export function FeaturesGrid(props: any) {
  const { setValue, goBot } = props;
  const features = prompts.map((feature, index) => (
    <Feature {...feature} key={index} setValue={setValue} goBot={goBot} />
  ));

  return (
    <Container>
      <SimpleGrid cols={{ base: 3, sm: 3, md: 3 }}>{features}</SimpleGrid>
    </Container>
  );
}
