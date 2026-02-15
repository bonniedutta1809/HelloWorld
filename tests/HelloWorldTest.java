```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class HelloWorldTest {

    @Test
    public void testMainOutput() {
        // Arrange
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outputStream));

        // Act
        HelloWorld.main(new String[]{});

        // Assert
        String output = outputStream.toString().trim();
        assertEquals("Hello, world!", output);

        // Restore the original System.out
        System.setOut(originalOut);
    }
}
```