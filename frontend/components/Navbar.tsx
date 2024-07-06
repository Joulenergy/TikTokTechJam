import { Group, Paper, Text, Title, UnstyledButton } from '@mantine/core';
import logo from '../public/navbar-logo.png';
import Image from 'next/image';
import ToggleColour from './ToggleColour';
import { useRouter } from 'next/router';

const NavBar = () => {
  const router = useRouter();

  const handleButtonClick = () => {
    // Navigate to the desired page here
    router.push('./');
  };

  return (
    <>
      <Paper radius={0}>
        <Group justify="apart" p="sm" align="center">
          <Text variant="gradient" gradient={{ from: 'orange', to: 'grape', deg: 90 }}>
            <Group align="center" gap={3}>
              <UnstyledButton onClick={handleButtonClick}>
                <Title>CommentSense</Title>
              </UnstyledButton>
              <Image height={30} width={30} src={logo} alt="CommentSense Logo" />
            </Group>
          </Text>
          <ToggleColour />
        </Group>
      </Paper>
    </>
  );
};

export default NavBar;
