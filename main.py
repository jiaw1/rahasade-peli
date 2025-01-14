import pygame
from random import randint, choice

class Rahasade:
    def __init__(self):
        pygame.init()
        self.leveys, self.korkeus = 640, 480
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.otsikko_fontti = pygame.font.SysFont("comicsansms", 50)
        self.ohje_fontti = pygame.font.SysFont("comicsansms", 20)
        self.fontti = pygame.font.SysFont("comicsansms", 24)

        self.lataa_kuvat()

        self.robo = self.kuvat[0]
        self.robo_x = 200
        self.robo_y = 480 - self.robo.get_height() - 30

        self.maataso = self.robo_y
        self.hyppy_korkeus = 120
        self.hyppy_nopeus = -15
        self.hyppaa = False
        self.hyppy_nopeus_nykyinen = 0

        self.oikealle = False
        self.vasemmalle = False

        self.pisteet = 0

        self.hirvio = self.kuvat[1]
        self.hirvio_maara = 1
        self.hirviot = self.luo_hirviot()

        self.kolikko = self.kuvat[2]
        self.kolikko_maara = 3
        self.kolikot = [[randint(0, self.leveys - self.kolikko.get_width()), -randint(100, 1000)] for _ in range(self.kolikko_maara)]

        self.kello = pygame.time.Clock()
        self.aloitus()

    def lataa_kuvat(self):
        self.kuvat = []
        for kuva in ["robo", "hirvio", "kolikko"]:
            self.kuvat.append(pygame.image.load(kuva + ".png"))

    def luo_hirviot(self):
        hirviot = []
        for _ in range(self.hirvio_maara):
            suunta = choice(["vasemmalta", "oikealta"])
            if suunta == "vasemmalta":
                x = -self.hirvio.get_width()
                nopeus = randint(3, 5)
            else:
                x = self.leveys
                nopeus = -randint(3, 5)
            hirviot.append([x, self.robo_y + 20, nopeus])
        return hirviot

    def piirra_naytto(self):
        self.naytto.fill("paleturquoise")
        teksti = self.fontti.render(f"Pisteet: {self.pisteet}", True, "darkblue")
        pygame.draw.rect(self.naytto, "darkseagreen", (0, 450, 640, 30))

        for i in range(self.kolikko_maara):
            self.kolikot[i][1] += 5

            if self.kolikot[i][1] > self.korkeus:
                self.kolikot[i][1] = -randint(100, 1000)
                self.kolikot[i][0] = randint(0, self.leveys - self.kolikko.get_width())

            if self.kolikot[i][1] + self.kolikko.get_height() >= self.robo_y:
                robo_keski = self.robo_x + self.robo.get_width() / 2
                kivi_keski = self.kolikot[i][0] + self.kolikko.get_width() / 2
                if abs(robo_keski - kivi_keski) <= (self.robo.get_width() + self.kolikko.get_width()) / 2:
                    self.kolikot[i][1] = -randint(100, 1000)
                    self.kolikot[i][0] = randint(0, self.leveys - self.kolikko.get_width())
                    self.pisteet += 1

        for kolikko in self.kolikot:
            self.naytto.blit(self.kolikko, kolikko)

        for hirvio in self.hirviot:
            hirvio[0] += hirvio[2]
            if hirvio[0] < -self.hirvio.get_width() or hirvio[0] > self.leveys:
                hirvio[0] = -self.hirvio.get_width() if hirvio[2] > 0 else self.leveys
                hirvio[2] = randint(3, 5) * (1 if hirvio[2] > 0 else -1)
            self.naytto.blit(self.hirvio, (hirvio[0], hirvio[1]))

            if abs(hirvio[0] - self.robo_x) < self.robo.get_width() and abs(hirvio[1] - self.robo_y) < self.robo.get_height():
                self.peli_paattyi()

        self.naytto.blit(teksti, (500, 30))
        self.naytto.blit(self.robo, (self.robo_x, self.robo_y))
        pygame.display.flip()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                pygame.quit()
                exit()

            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_SPACE and not self.hyppaa:
                    self.hyppaa = True
                    self.hyppy_nopeus_nykyinen = self.hyppy_nopeus

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False

        if self.oikealle and self.robo_x < self.leveys - self.robo.get_width():
            self.robo_x += 10
        if self.vasemmalle and self.robo_x > 0:
            self.robo_x -= 10

        if self.hyppaa:
            self.robo_y += self.hyppy_nopeus_nykyinen
            self.hyppy_nopeus_nykyinen += 0.6
            if self.robo_y >= self.maataso:
                self.robo_y = self.maataso
                self.hyppaa = False

    def peli_paattyi(self):
        self.naytto.fill("paleturquoise")
        teksti = self.otsikko_fontti.render("Peli päättyi!", True, "darkblue")
        tulosteksti = self.fontti.render(f"Sait {self.pisteet} pistettä.", True, "darkblue")
        paluuteksti = self.fontti.render("Siirrytään aloitussivulle...", True, "darkblue")
        self.naytto.blit(teksti, (170, 150))
        self.naytto.blit(tulosteksti, (170, 250))
        self.naytto.blit(paluuteksti, (170, 300))
        pygame.display.flip()
        pygame.time.wait(3500)
        self.aloitus()

    def aloitus(self):
        while True:
            self.naytto.fill("paleturquoise")
            otsikko = self.otsikko_fontti.render("Rahasade-peli", True, "darkblue")
            ohjeet = [
                "Ohjeet:",
                "",
                "1. Auta robottia keräämään taivaalta tippuvia kolikoita.",
                "2. Ohjaa robottia nuolinäppäimillä (vasen / oikea).",
                "3. Vältä vaakasuunnasta tulevia hirviöitä.",
                "4. Hyppää hirviön yli SPACE-näppäimellä.",
                "5. Peli päättyy, kun robotti osuu hirviöön.",
                "",
                "Aloita peli painamalla ENTER."
            ]

            self.naytto.blit(otsikko, (self.leveys // 2 - otsikko.get_width() // 2, 50))

            for i, rivi in enumerate(ohjeet):
                teksti = self.ohje_fontti.render(rivi, True, "darkblue")
                self.naytto.blit(teksti, (50, 150 + i * 30))

            pygame.display.flip()

            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if tapahtuma.type == pygame.KEYDOWN and tapahtuma.key == pygame.K_RETURN:
                    self.peli_kayntiin()

    def peli_kayntiin(self):
        self.pisteet = 0
        self.robo_x = 200
        self.kolikot = [[randint(0, self.leveys - self.kolikko.get_width()), -randint(100, 1000)] for _ in range(self.kolikko_maara)]
        self.hirviot = self.luo_hirviot()
        while True:
            self.piirra_naytto()
            self.tutki_tapahtumat()
            self.kello.tick(60)

if __name__ == "__main__":
    Rahasade()
