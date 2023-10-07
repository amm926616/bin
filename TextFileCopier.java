import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class TextFileCopier extends Application {
    private String[] lines;
    private int currentIndex = 0;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Easy Paste Developed By AD178");

        FileChooser fileChooser = new FileChooser();
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Text Files", "*.txt"));

        Button chooseFileButton = new Button("Choose File");
        chooseFileButton.setOnAction(e -> chooseFile(fileChooser, primaryStage));

        TextArea textDisplay = new TextArea();
        textDisplay.setEditable(false);
        textDisplay.setPrefSize(400, 200);

        VBox vbox = new VBox(10);
        vbox.getChildren().addAll(chooseFileButton, textDisplay);

        Scene scene = new Scene(vbox, 400, 250);
        primaryStage.setScene(scene);

        primaryStage.show();
    }

    private void chooseFile(FileChooser fileChooser, Stage primaryStage) {
        File file = fileChooser.showOpenDialog(primaryStage);

        if (file != null) {
            currentIndex = 0;
            readLinesFromFile(file);
            copyLineToClipboard();
        }
    }

    private void readLinesFromFile(File file) {
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            StringBuilder content = new StringBuilder();

            while ((line = reader.readLine()) != null) {
                content.append(line).append("\n");
            }

            lines = content.toString().split("\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void copyLineToClipboard() {
        if (lines != null && currentIndex >= 0 && currentIndex < lines.length) {
            String line = lines[currentIndex].trim();
            javafx.scene.input.Clipboard clipboard = javafx.scene.input.Clipboard.getSystemClipboard();
            javafx.scene.input.ClipboardContent content = new javafx.scene.input.ClipboardContent();
            content.putString(line);
            clipboard.setContent(content);
        }
    }

    public void incrementIndex() {
        if (lines != null && currentIndex < lines.length - 1) {
            currentIndex++;
            copyLineToClipboard();
        }
    }

    public void decrementIndex() {
        if (lines != null && currentIndex > 0) {
            currentIndex--;
            copyLineToClipboard();
        }
    }

    public void copyLine() {
        copyLineToClipboard();
    }
}
