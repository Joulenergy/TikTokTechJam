import { Alert, Group, Stack } from '@mantine/core';
import Image from 'next/image';
import logo from '../public/orange.png';
import replylogo from '../public/purple.png';

const ChatMessage = (props: any) => {
  const { text, user } = props;
  const message = user ? 'right' : 'left';
  let color;

  if (message === 'right') {
    color = 'indigo';
  }
  if (message === 'left') {
    color = 'yellow';
  }

  return (
    <>
      <Group position={message} align="flex-end">
        <Stack p={0} spacing={2} sx={{ maxWidth: '80%' }} align="flex-end">
          <Group position={message} align="flex-end" spacing="xs">
            <Image
              src={logo}
              height={35}
              width={30}
              alt="CommentSense Bot"
              hidden={message === 'right' ? true : false}
            />
            <Stack p={0} spacing={0} m={0}>
              <Group position={message} spacing={3} align="center">
                <Alert sx={{}} color={color} radius="lg" py={8} variant="light">
                  {text}
                </Alert>
              </Group>
            </Stack>
            <Image
              src={replylogo}
              height={35}
              width={30}
              alt="Prompter Logo"
              hidden={message === 'right' ? false : true}
            />
          </Group>
        </Stack>
      </Group>
    </>
  );
};

export default ChatMessage;
