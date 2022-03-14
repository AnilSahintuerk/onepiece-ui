import React from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Button,
  Stack,
  FormControl,
  FormLabel,
  Grid,
  Input,
  Container,
  extendTheme,
} from '@chakra-ui/react';

const colors = {
  op: {
    900: '#A7C4D8',
    800: '#356FB0',
    700: '#336AAC',
    600: '#5FBDF4',
  },
};

const theme = extendTheme({ colors });

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Box
        bg="linear-gradient(180deg, #5FBDF4 0%, #336AAC 100%)"
        w="100vw"
        h="100vh"
      >
        <Container bg="white" maxW="container.lg" h="100%" centerContent>
          <Box pr={32} pl={32} minWidth="30rem">
            <img src="op_logo.png" />
          </Box>
          <Stack w="50%" minW="20rem" spacing={15}>
            <FormControl>
              <FormLabel>E-Mail</FormLabel>
              <Input bg="op.900" />
            </FormControl>
            <FormControl>
              <FormLabel>Chapter</FormLabel>
              <Input bg="op.900" />
            </FormControl>
            <Button bg="op.800" color="white">
              Get Chapter
            </Button>
          </Stack>
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;
