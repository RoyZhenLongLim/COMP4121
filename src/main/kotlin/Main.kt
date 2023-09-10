fun main(args: Array<String>) {
    do {
        val input = readln()
        when (input) {
            "1" -> println("hi")
            "" -> print("Terminating Program")
            else -> println("Invalid Command")
        }
    } while (input.isNotEmpty())
}