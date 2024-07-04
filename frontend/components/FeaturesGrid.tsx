import { ThemeIcon, Text, Title, Container, SimpleGrid, rem } from '@mantine/core';
import { IconGauge, IconCookie, IconUser, IconMessage2, IconLock } from '@tabler/icons-react';
import classes from './FeaturesGrid.module.css';

export const MOCKDATA = [
  {
    icon: IconGauge,
    title: 'suggestion1',
    description:
      'nomnomnom nomnomnom nomnomnom nomnomnom',
  },
  {
    icon: IconUser,
    title: 'suggestion2',
    description:
      'omnomnomn omnomnomn omnomnomn omnomnomn',
  },
  {
    icon: IconCookie,
    title: 'suggestion3',

    description:
      'hehehehehe hehehehehe hehehehehe hehehehehe',
  },
  {
    icon: IconCookie,
    title: 'suggestion4',
    description:
      'hehehehehe hehehehehe hehehehehe hehehehehe',
  }

];

interface FeatureProps {
  icon: React.FC<any>;
  title: React.ReactNode;
  description: React.ReactNode;
}

export function Feature({ icon: Icon, title, description }: FeatureProps) {
  return (
    <div>
      <ThemeIcon variant="light" size={40} radius={40}>
        <Icon style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
      </ThemeIcon>
      <Text mt="sm" mb={7}>
        {title}
      </Text>
      <Text size="sm" c="dimmed" lh={1.6}>
        {description}
      </Text>
    </div>
  );
}

export function FeaturesGrid() {
  const features = MOCKDATA.map((feature, index) => <Feature {...feature} key={index} />);

  return (
    <Container className={classes.wrapper}>
      <SimpleGrid
        mt={60}
        cols={{ base: 1, sm: 2, md: 3 }}
        // spacing={{ base: 'xl', md: 50 }}
        // verticalSpacing={{ base: 'xl', md: 50 }}
      >
        {features}
      </SimpleGrid>
    </Container>
  );
}