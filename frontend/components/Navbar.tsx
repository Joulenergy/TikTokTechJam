import { Group, Paper, Text, Title, UnstyledButton } from '@mantine/core';
import logo from '../public/navbar-logo.png';
import Image from 'next/image';
import DarkMode from './DarkMode';
import { useRouter } from 'next/router';

const NavBar = () => {
  const router = useRouter();

  const handleButtonClick = () => {
    // Navigate to the desired page here
    router.push('./');
  };

  return (
    <>
      <Paper radius={0} sx={{ boxShadow: '0px 2px 0px 0px rgba(173,181,189,.5)' }}>
        <Group position="apart" p="sm" align="center" sx={{ height: '8vh' }}>
          <Text variant="gradient" gradient={{ from: 'grape', to: 'cyan', deg: 90 }}>
            <Group align="center" spacing={3}>
              <UnstyledButton onClick={handleButtonClick}>
                <Title>CommentSense</Title>
              </UnstyledButton>
              <Image height={30} width={30} src={logo} alt="CommentSense Logo" />
            </Group>
          </Text>
          <DarkMode />
        </Group>
      </Paper>
    </>
  );
};

export default NavBar;
