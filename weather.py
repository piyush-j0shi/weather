from tqdm import tqdm
import time


def weather():
    check_weather = input("do you want to check weather now : yes / no : ")

    if check_weather.lower().strip() == "yes":
        current_city = input("enter you current city : ")

        print("getting the current weather, it will take 10 seconds so hold on tight.")

        for i in tqdm(range(int(100))):
            time.sleep(0.1)

        print("look out of your fucking window you fucking Dumbass.")

    elif check_weather.lower().strip() == "no":
        print("why the fuck are you here then, you fucking piece of shit.")

    else:
        print(
            "are you fucking retarted you fucking pig, can't you see yes or no, are you fucking blind."
        )


if __name__ == "__main__":
    weather()
