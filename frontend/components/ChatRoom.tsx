import { ActionIcon, Group, Paper, ScrollArea, Stack, Container } from '@mantine/core';
import { useEffect, useRef, useState } from 'react';
import { useInView } from 'react-intersection-observer';
import { ChevronDown } from 'tabler-icons-react';
import ChatMessage from './ChatMessage';
import Loading from './Loading';
import ChatInput from './ChatInput';
import { FeaturesGrid } from './FeaturesGrid';
import NavBar from './Navbar';

const ChatRoom = () => {
  const [mes, setMes] = useState<any[]>([]);
  const [loading, setloading] = useState(true);
  const dummy = useRef<HTMLDivElement>(null);

  // get messages on 500ms after page load
  useEffect(() => {
    setTimeout(() => {
      getMessages();
    }, 500);
    // eslint-disable-next-line
  }, []);

  const getMessages = () => {
    const exists = localStorage.getItem('messages');
    if (exists) {
      const messages = JSON.parse(exists);
      setMes(messages);
    } else {
      addMessage(
        'Hello, I am CommentSense, your content crafting companion! What would you like to explore about the video(s)?',
        true
      );
    }
    setloading(false);
    setTimeout(() => {
      goBot();
    }, 300);
  };

  const addMessage = (mess: string, bot = false) => {
    const exists = localStorage.getItem('messages');
    const messages = exists ? JSON.parse(exists) : [];
    messages.push({ message: mess, user: !bot });
    localStorage.setItem('messages', JSON.stringify(messages));
    setMes(messages);
    // TODO: get chatbot reply from backend
  };

  function goBot() {
    dummy.current?.scrollIntoView({ behavior: 'smooth' });
  }

  const [value, setValue] = useState('');

  const { ref, inView } = useInView({
    /* Optional options */
    delay: 600,
    threshold: 1,
  });

  return (
    <>
      {loading ? (
        <Loading />
      ) : (
        <>
          <Container size="800px" mx="auto">
            <NavBar />
            <Stack sx={{ height: '84vh' }} p={0}>
              <ScrollArea p="xs" scrollbarSize={1} sx={{ height: '84vh' }}>
                <Stack>
                  <Group hidden={inView} position="center" pt="xs">
                    <Paper
                      shadow="md"
                      radius="xl"
                      withBorder
                      p={0}
                      sx={{ position: 'absolute', top: '95%' }}
                    >
                      <ActionIcon color="violet" radius="xl" onClick={goBot}>
                        <ChevronDown />
                      </ActionIcon>
                    </Paper>
                    <FeaturesGrid setValue={setValue} goBot={goBot}/>
                  </Group>

                  {mes.map((msg, id) => {
                    return <ChatMessage key={id} text={msg.message} user={msg.user} />;
                  })}
                </Stack>
                <div ref={ref}></div>
                <div ref={dummy}></div>
              </ScrollArea>
            </Stack>
            <ChatInput setValue={setValue} value={value} fn={goBot} addMessage={addMessage} />
          </Container>
        </>
      )}
    </>
  );
};
export default ChatRoom;