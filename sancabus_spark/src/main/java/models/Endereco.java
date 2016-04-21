package models;

/**
 * Created by Henrique on 2/04/2016.
 */
public class Endereco {

    private String linha;
    private int ordem;
    private int idavolta;
    private String endereco;


    public String getLinha() {
        return linha;
    }

    public void setLinha(String linha) {
        this.linha = linha;
    }

    public int getOrdem() {
        return ordem;
    }

    public void setOrdem(int ordem) {
        this.ordem = ordem;
    }

    public int getIdavolta() {
        return idavolta;
    }

    public void setIdavolta(int idavolta) {
        this.idavolta = idavolta;
    }

    public String getEndereco() {
        return endereco;
    }

    public void setEndereco(String endereco) {
        this.endereco = endereco;
    }
}
