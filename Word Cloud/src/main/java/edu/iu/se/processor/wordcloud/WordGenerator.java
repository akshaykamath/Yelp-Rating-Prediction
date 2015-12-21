package edu.iu.se.processor.wordcloud;

import java.awt.Color;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

import wordcloud.CollisionMode;
import wordcloud.LayeredWordCloud;
import wordcloud.PolarBlendMode;
import wordcloud.PolarWordCloud;
import wordcloud.WordCloud;
import wordcloud.WordFrequency;
import wordcloud.bg.CircleBackground;
import wordcloud.bg.PixelBoundryBackground;
import wordcloud.bg.RectangleBackground;
import wordcloud.font.CloudFont;
import wordcloud.font.FontWeight;
import wordcloud.font.scale.SqrtFontScalar;
import wordcloud.image.AngleGenerator;
import wordcloud.nlp.FrequencyAnalyzer;
import wordcloud.palette.ColorPalette;

public class WordGenerator
{
	final static String inputDirBase = "C:\\Users\\pratish\\Documents\\data\\wordcloud\\input\\";
	final static String outputDirBase = "C:\\Users\\pratish\\Documents\\data\\wordcloud\\output\\";
	final static String background_dir = "C:\\Users\\pratish\\Documents\\data\\wordcloud\\background\\";

	final static int defaultMinFont = 15;
	final static int defaultMaxFont = 90;

	public static void main(String[] args) throws IOException
	{

		WordGenerator generator = new WordGenerator();

		String positiveInput = inputDirBase + "MostOccPostiveWords.txt";
		String negativeInput = inputDirBase + "MostOccNegativeWords.txt";
		String mostPositiveInput = inputDirBase + "MostPostiveWords.txt";
		String mostNegativeInput = inputDirBase + "MostNegativeWords.txt";

		List<WordFrequency> positiveWordFrequencies = generator.getFrequency(positiveInput);
		List<WordFrequency> negativeWordFrequencies = generator.getFrequency(negativeInput);
		List<WordFrequency> mpositiveWordFrequencies = generator
				.getFrequencyFromScore(mostPositiveInput);
		List<WordFrequency> mnegativeWordFrequencies = generator
				.getFrequencyFromScore(mostNegativeInput);

		/*
		 * generator.generateCircleWordCloud(positiveWordFrequencies,
		 * outputDirBase + "positive_circle.png");
		 * generator.generateCircleWordCloud(negativeWordFrequencies,
		 * outputDirBase + "negative_circle.png");
		 * generator.generateCircleWordCloud(mpositiveWordFrequencies,
		 * outputDirBase + "most_positive_circle.png", 15, 50);
		 * generator.generateCircleWordCloud(mnegativeWordFrequencies,
		 * outputDirBase + "most_negative_circle.png", 15, 50);
		 */

		generator.generateLayeredWordCloudRectangle(positiveWordFrequencies,
				negativeWordFrequencies, outputDirBase + "layered.png");
		generator.generateLayeredWordCloudRectangle(mpositiveWordFrequencies,
				mnegativeWordFrequencies, outputDirBase + "layered_most.png");
	}

	public List<WordFrequency> getFrequency(String fileName) throws FileNotFoundException
	{
		List<WordFrequency> wordFrequencies = new ArrayList<WordFrequency>();

		Scanner sc = new Scanner(new File(fileName));

		while (sc.hasNext())
		{
			String line = sc.nextLine();
			if (!line.trim().isEmpty())
			{
				String[] tokens = line.split(";");
				WordFrequency frequency = new WordFrequency(tokens[0], Integer.parseInt(tokens[1]));
				wordFrequencies.add(frequency);
			}
		}

		sc.close();
		return wordFrequencies;
	}

	public List<WordFrequency> getFrequencyFromScore(String fileName) throws FileNotFoundException
	{
		List<WordFrequency> wordFrequencies = new ArrayList<WordFrequency>();

		Scanner sc = new Scanner(new File(fileName));

		while (sc.hasNext())
		{
			String line = sc.nextLine();
			Random random = new Random();
			if (!line.trim().isEmpty())
			{
				String[] tokens = line.split(";");
				String word = tokens[0];
				Double score = Double.valueOf(tokens[1]) * (random.nextInt(1000) + 1);
				WordFrequency frequency = new WordFrequency(word, score.intValue());
				wordFrequencies.add(frequency);
			}
		}

		sc.close();
		return wordFrequencies;
	}

	public void generateCircleWordCloud(String inputFiule, String outPutFile) throws IOException
	{
		File sampleFile = new File(inputFiule);
		FileInputStream stream = new FileInputStream(sampleFile);
		final FrequencyAnalyzer frequencyAnalyzer = new FrequencyAnalyzer();
		frequencyAnalyzer.setWordFrequencesToReturn(500);
		final List<WordFrequency> wordFrequencies = frequencyAnalyzer.load(stream);

		final WordCloud wordCloud = new WordCloud(600, 600, CollisionMode.PIXEL_PERFECT);
		wordCloud.setPadding(2);
		wordCloud.setBackground(new CircleBackground(300));
		wordCloud.setColorPalette(
				new ColorPalette(new Color(0x4055F1), new Color(0x408DF1), new Color(0x40AAF1),
						new Color(0x40C5F1), new Color(0x40D3F1), new Color(0xFFFFFF)));
		wordCloud.setFontScalar(new SqrtFontScalar(10, 60));
		wordCloud.build(wordFrequencies);
		wordCloud.writeToFile(outPutFile);
	}

	public void generateLayeredWordCloud(final List<WordFrequency> positiveWordFrequencies,
			final List<WordFrequency> negativeWordFrequencies, String outputFile) throws IOException
	{

		File positiveBg = new File(background_dir + "cloud_bg.bmp");
		File negativeBg = new File(background_dir + "cloud_fg.bmp");

		final LayeredWordCloud layeredWordCloud = new LayeredWordCloud(2, 1200, 600,
				CollisionMode.PIXEL_PERFECT);

		layeredWordCloud.setPadding(0, 1);
		layeredWordCloud.setPadding(1, 1);

		layeredWordCloud.setFontOptions(0, new CloudFont("LICENSE PLATE", FontWeight.BOLD));
		layeredWordCloud.setFontOptions(1, new CloudFont("Comic Sans MS", FontWeight.BOLD));

		layeredWordCloud.setBackground(0,
				new PixelBoundryBackground(new FileInputStream(positiveBg)));
		layeredWordCloud.setBackground(1,
				new PixelBoundryBackground(new FileInputStream(negativeBg)));

		layeredWordCloud.setColorPalette(0,
				new ColorPalette(new Color(0xABEDFF), new Color(0x82E4FF), new Color(0x55D6FA)));
		layeredWordCloud.setColorPalette(1,
				new ColorPalette(new Color(0xFFFFFF), new Color(0xDCDDDE), new Color(0xCCCCCC)));

		layeredWordCloud.setFontScalar(0, new SqrtFontScalar(10, 80));
		layeredWordCloud.setFontScalar(1, new SqrtFontScalar(10, 80));

		layeredWordCloud.build(0, positiveWordFrequencies);
		layeredWordCloud.build(1, negativeWordFrequencies);
		layeredWordCloud.writeToFile(outputFile);
	}

	public void generateLayeredWordCloudRectangle(final List<WordFrequency> positiveWordFrequencies,
			final List<WordFrequency> negativeWordFrequencies, String outputFile) throws IOException
	{

		final PolarWordCloud polarWordCloud = new PolarWordCloud(1200, 600,
				CollisionMode.PIXEL_PERFECT, PolarBlendMode.BLUR);
		polarWordCloud.setPadding(2);
		polarWordCloud.setCloudFont(new CloudFont("LICENSE PLATE", FontWeight.BOLD));

		polarWordCloud.setBackground(new RectangleBackground(1200, 600));
		polarWordCloud.setBackgroundColor(Color.gray);

		polarWordCloud.setFontScalar(new SqrtFontScalar(10, 80));
		polarWordCloud.build(positiveWordFrequencies, negativeWordFrequencies);
		polarWordCloud.writeToFile(outputFile);
	}

	public void generateCircleWordCloud(final List<WordFrequency> wordFrequencies,
			String outPutFile) throws IOException
	{
		generateCircleWordCloud(wordFrequencies, outPutFile, defaultMinFont, defaultMaxFont);
	}

	public void generateCircleWordCloud(final List<WordFrequency> wordFrequencies,
			String outPutFile, int minFont, int maxFont) throws IOException
	{
		final WordCloud wordCloud = new WordCloud(800, 800, CollisionMode.PIXEL_PERFECT);
		wordCloud.setPadding(2);
		wordCloud.setBackground(new RectangleBackground(400));
		wordCloud.setBackgroundColor(Color.WHITE);
		wordCloud.setColorPalette(new ColorPalette(new Color(Color.BLUE.getRGB()),
				new Color(Color.GREEN.getRGB()), new Color(Color.ORANGE.getRGB())));
		wordCloud.setFontScalar(new SqrtFontScalar(15, 50));
		wordCloud.build(wordFrequencies);
		wordCloud.writeToFile(outPutFile);
	}
}
