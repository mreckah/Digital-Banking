package com.hospital.Hospital.entities;


import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.*;

import java.util.Date;

@Entity
@Data @Getter @Setter @NoArgsConstructor
@AllArgsConstructor @Builder

public class Patient {
    @Id @GeneratedValue(strategy= GenerationType.IDENTITY)
    private int id;
    private String name;
    private Date dateOfBirth;
    private String sick;
    private int score;
}
