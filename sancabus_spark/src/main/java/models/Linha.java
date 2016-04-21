package models;

import java.util.List;

/**
 * Created by Henrique on 2/04/2016.
 */
public class Linha {

    private String numero;
    private String nome;
    private String link;
    private String horarioIda;
    private String horarioVolta;

    private List<Endereco> enderecosIda;
    private List<Endereco> enderecosVolta;

    public String getNumero() {
        return numero;
    }

    public void setNumero(String numero) {
        this.numero = numero;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getLink() {
        return link;
    }

    public void setLink(String link) {
        this.link = link;
    }

    public String getHorarioIda() {
        return horarioIda;
    }

    public void setHorarioIda(String horarioIda) {
        this.horarioIda = horarioIda;
    }

    public String getHorarioVolta() {
        return horarioVolta;
    }

    public void setHorarioVolta(String horarioVolta) {
        this.horarioVolta = horarioVolta;
    }

    public List<Endereco> getEnderecosIda() {
        return enderecosIda;
    }

    public void setEnderecosIda(List<Endereco> enderecosIda) {
        this.enderecosIda = enderecosIda;
    }

    public List<Endereco> getEnderecosVolta() {
        return enderecosVolta;
    }

    public void setEnderecosVolta(List<Endereco> enderecosVolta) {
        this.enderecosVolta = enderecosVolta;
    }
}
