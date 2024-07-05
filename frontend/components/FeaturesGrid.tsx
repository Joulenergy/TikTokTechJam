import { useMantineColorScheme, ThemeIcon, Text, Container, SimpleGrid, rem } from '@mantine/core';
import { IconGauge, IconCookie, IconUser } from '@tabler/icons-react';
import classes from './FeaturesGrid.module.css';

export const MOCKDATA = [
  {
    icon: IconGauge,
    title: 'summarise video comments',
  },
  {
    icon: IconUser,
    title: 'conduct sentiment analysis',
  },
  {
    icon: IconCookie,
    title: 'suggest new ideas for future videos',
  },
];

interface FeatureProps {
  icon: React.FC<any>;
  title: React.ReactNode;
}

export function Feature({ icon: Icon, title }: FeatureProps) {
  const { colorScheme } = useMantineColorScheme();
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

export function FeaturesGrid() {
  const features = MOCKDATA.map((feature, index) => <Feature {...feature} key={index} />);

  return (
    <Container>
      <SimpleGrid
        cols={{ base: 1, sm: 2, md: 3 }}
        // spacing={{ base: 'xl', md: 50 }}
        // verticalSpacing={{ base: 'xl', md: 50 }}
      >
        {features}
      </SimpleGrid>
    </Container>
  );
}
