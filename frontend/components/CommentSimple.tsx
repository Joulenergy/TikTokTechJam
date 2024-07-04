import { Text, Group } from '@mantine/core';
import logo from '../public/orange.png';
import Image from 'next/image'

export function CommentSimple() {
  return (
    <div style={{ padding: '10px' }}>
      <Group>
        <Image src={logo}  height={35} width={30} alt="CommentSense Bot" />
        <Text size="sm">The comments are mostly happy</Text>
      </Group>
    </div>
  );
}
