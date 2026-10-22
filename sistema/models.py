from django.db import models
from django.core.validators import MinValueValidator


class Login(models.Model):
    CARGOS = [
        ("Admin", "Admin"),
        ("Gerente", "Gerente"),
        ("Motorista", "Motorista"),
    ]

    id_login = models.AutoField(primary_key=True)  
    usuario = models.CharField(max_length=50, unique=True)
    cargo = models.CharField(max_length=50, choices=CARGOS)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = "login"

    def __str__(self):
        return self.usuario


class Veiculo(models.Model):
    COMBUSTIVEIS = [
        ("Elétrico", "Elétrico"),
        ("Diesel", "Diesel"),
    ]

    STATUS = [
        ("Disponível", "Disponível"),
        ("Em rota", "Em rota"),
        ("Em rota parcial", "Em rota parcial"),
        ("Em manutenção", "Em manutenção"),
    ]

    id_veiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=8, unique=True)
    numero_frota = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=10)
    modelo = models.CharField(max_length=50)
    combustivel = models.CharField(
        max_length=10,
        choices=COMBUSTIVEIS
    )
    capacidade = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Disponível"
    )

    class Meta:
        db_table = "veiculo"

    def __str__(self):
        return f"{self.numero_frota} - {self.modelo}"


class Motorista(models.Model):
    id_motorista = models.AutoField(primary_key=True)
    cnh = models.CharField(max_length=20, unique=True)
    categoria_cnh = models.CharField(max_length=3)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)

    id_login = models.OneToOneField(
        Login,
        on_delete=models.CASCADE,
        db_column="id_login"
    )

    id_veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="id_veiculo"
    )

    class Meta:
        db_table = "motorista"

    def __str__(self):
        return self.nome


class Manutencao(models.Model):
    TIPOS = [
        ("Preventiva", "Preventiva"),
        ("Corretiva", "Corretiva"),
    ]

    id_manutencao = models.AutoField(primary_key=True)
    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )
    local = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    descricao = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    custo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    data_entrada = models.DateField()
    data_saida = models.DateField(
        null=True,
        blank=True
    )

    id_veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        db_column="id_veiculo"
    )

    class Meta:
        db_table = "manutencao"

    def __str__(self):
        return f"{self.tipo} - {self.id_veiculo}"