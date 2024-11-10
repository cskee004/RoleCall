package com.rolecall;
//Extremely Empty Boiler plate Listing class for testing
public class Listing {
    private int id;
    private String name;

    public Listing(int id, String name){
        this.id = id;
        this.name =name;
    }
    public Listing(String json){
        String[] attributes = json.substring(1).split(",");
        for (String attribute : attributes){
            String[] values = attribute.split(":");
            switch(values[0]){
                case "\"id\"":
                    this.id = Integer.parseInt(values[1]);
                    break;
                case "\"name\"":
                    this.name = values[1];
                    break;
            }
        }
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }
}
