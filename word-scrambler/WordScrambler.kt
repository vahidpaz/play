import java.io.File
import kotlin.system.exitProcess

/**
 * Rearranges the order of letters in a text file, while remaining humanly legible. It's fun :)
 *
 * The human mind is capable of deciphering words even when the letters
 * in the middle of the words have been rearranged. Keeping the first and
 * last letters stationary, the others can be shuffled around.
 *
 * Given a text file, this class will scramble all its words and save the result
 * to the specified output file. The file size of the output will match that
 * of the input.
 *
 * This class supports unicode characters, thus other languages beyond
 * English should be supported. However, this has not been extensively tested.
 *
 * The `scrambleWord()` function is also provided for users to
 * rearrange the letters of their own words.
 */
data class WordScrambler(val inputFile: String, val outputFile: String) {

    companion object {
        fun scrambleWord(word: String): String {
            val alphabeticWord = "(?U)\\p{IsAlphabetic}+".toRegex()
            if (word.length <= 3 || !word.matches(alphabeticWord)) return word

            val middle = word.substring(1, word.length - 1).asIterable()
            return word.first() + middle.shuffled().joinToString("") + word.last()
        }
    }

    private fun scrambleLine(line: String): String {
        // Supports unicode ("U" flag). Match words and non-words.
        val wordRegex = "(?U)(\\w+)|([^\\w]+)".toRegex()
        val sb = StringBuilder()

        val tokens = wordRegex.findAll(line)
            .map {
                // groupValues[0] is the whole match, not an actual group.
                val word = it.groupValues[1]
                val nonWord = it.groupValues[2]
                if (word.isNotEmpty()) word else nonWord
            }

        tokens.forEach {
            val scrambled = scrambleWord(it)
            assert(scrambled.toSortedSet() == it.toSortedSet())
            sb.append(scrambled)
        }

        sb.append("\n")
        return sb.toString()
    }

    fun scramble() {
        File(outputFile).bufferedWriter().use { writer ->
            File(inputFile).bufferedReader().forEachLine { line ->
                writer.write(scrambleLine(line))
            }
        }
        assert(File(inputFile).length() == File(outputFile).length())
    }
}

fun main(args: Array<String>) {
    if (args.size != 2) {
        println("Syntax error.\nPlease use the following arguments: <input_filename> <output_filename>")
        exitProcess(1)
    }

    WordScrambler(args[0], args[1]).scramble()
}
